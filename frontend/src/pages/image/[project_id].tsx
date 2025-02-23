import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import FlowerView from '@/components/layout/FlowerView';
import { useModel } from '@/contexts/ModelContext';
import BackgroundWrapper from '@/components/layout/FlowerViews/BackgroundWrapper';
import { getModelById } from '@/services/api';

const ProjectPage = () => {
  const router = useRouter();
  const { project_id } = router.query;
  const { model, setModel } = useModel();

  useEffect(() => {
    const loadModel = async () => {
      if (project_id && !model) {
        try {
          const fetchedModel = await getModelById(project_id as string);
          setModel(fetchedModel);
        } catch (error) {
          console.error('Error loading model:', error);
          router.push('/'); // Redirect to home on error
        }
      }
    };

    loadModel();
  }, [project_id, model, setModel, router]);

  if (!model) {
    return <div>Loading...</div>; // Add a proper loading state
  }

  return (
    <BackgroundWrapper>
      <FlowerView />
    </BackgroundWrapper>
  );
};

export default ProjectPage;
